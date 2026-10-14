import getpass
import os

try:
    import oracledb
except ImportError:
    oracledb = None

DSN_PADRAO = "oracle.fiap.com.br:1521/ORCL"

SQL_CRIAR = """
CREATE TABLE colheita_cafe (
    id        NUMBER PRIMARY KEY,
    talhao    VARCHAR2(30) NOT NULL,
    metodo    VARCHAR2(10) NOT NULL,
    area      NUMBER(10,2) NOT NULL,
    estimada  NUMBER(10,2) NOT NULL,
    colhida   NUMBER(10,2) NOT NULL,
    preco     NUMBER(10,2) NOT NULL
)
"""

SQL_SALVAR = """
MERGE INTO colheita_cafe t
USING (SELECT :id AS id FROM dual) s ON (t.id = s.id)
WHEN MATCHED THEN UPDATE SET talhao = :talhao, metodo = :metodo, area = :area,
    estimada = :estimada, colhida = :colhida, preco = :preco
WHEN NOT MATCHED THEN INSERT (id, talhao, metodo, area, estimada, colhida, preco)
    VALUES (:id, :talhao, :metodo, :area, :estimada, :colhida, :preco)
"""


def conectar():
    if oracledb is None:
        raise RuntimeError("Biblioteca oracledb nao instalada (pip install oracledb).")
    usuario = os.getenv("ORACLE_USER") or input("  Usuario Oracle: ").strip()
    senha = os.getenv("ORACLE_PASSWORD") or getpass.getpass("  Senha Oracle: ")
    dsn = os.getenv("ORACLE_DSN", DSN_PADRAO)
    return oracledb.connect(user=usuario, password=senha, dsn=dsn)


def criar_tabela(conexao):
    with conexao.cursor() as cursor:
        try:
            cursor.execute(SQL_CRIAR)
        except oracledb.DatabaseError as erro:
            if "ORA-00955" not in str(erro):
                raise


def enviar_lotes(lotes):
    conexao = conectar()
    try:
        criar_tabela(conexao)
        with conexao.cursor() as cursor:
            for lote in lotes:
                cursor.execute(SQL_SALVAR, {
                    "id": lote["id"], "talhao": lote["talhao"], "metodo": lote["metodo"],
                    "area": lote["area"], "estimada": lote["estimada"],
                    "colhida": lote["colhida"], "preco": lote["preco"],
                })
        conexao.commit()
        return len(lotes)
    finally:
        conexao.close()


def buscar_lotes():
    conexao = conectar()
    try:
        criar_tabela(conexao)
        with conexao.cursor() as cursor:
            cursor.execute(
                "SELECT id, talhao, metodo, area, estimada, colhida, preco "
                "FROM colheita_cafe ORDER BY id"
            )
            return [
                {"id": int(i), "talhao": t, "metodo": m, "area": float(a),
                 "estimada": float(e), "colhida": float(c), "preco": float(p)}
                for i, t, m, a, e, c, p in cursor.fetchall()
            ]
    finally:
        conexao.close()
