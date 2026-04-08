from neo4j import AsyncDriver
from app.db.neo4j import get_driver
from app.schemas.agriculture import MedicineInfo, PestInfo

_QUERY = """
MATCH (p:Pest {name: $name})-[:TREATED_BY]->(m:Medicine)
RETURN p.name        AS pest_name,
       p.common_name AS common_name,
       p.affected_crops AS affected_crops,
       m.name        AS medicine_name,
       m.dosage      AS dosage,
       m.description AS description
"""


async def get_pest_treatments(pest_name: str) -> PestInfo | None:
    driver: AsyncDriver = await get_driver()
    async with driver.session() as session:
        result = await session.run(_QUERY, name=pest_name)
        records = await result.data()

    if not records:
        return None

    first = records[0]
    treatments = [
        MedicineInfo(
            name=rec["medicine_name"],
            dosage=rec.get("dosage"),
            description=rec.get("description"),
        )
        for rec in records
        if rec.get("medicine_name")
    ]

    return PestInfo(
        name=first["pest_name"],
        common_name=first.get("common_name"),
        affected_crops=first.get("affected_crops") or [],
        treatments=treatments,
    )
