from dataclasses import dataclass

@dataclass
class PaqueteMetadata:
    """
    Molde de datos estricto para el MVP. 
    Solo contiene la información pública (metadatos) que viajará a Supabase.
    No incluye nombres de archivos originales ni contraseñas.
    """
    id: str
    tamano_bytes: int
    creado_en: str
    expira_en: str
    descargas_actuales: int = 0
    limite_descargas: int = 1
    estado: str = "activo"

    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario para poder guardarlo en Supabase."""
        return {
            "id": self.id,
            "tamano_bytes": self.tamano_bytes,
            "creado_en": self.creado_en,
            "expira_en": self.expira_en,
            "descargas_actuales": self.descargas_actuales,
            "limite_descargas": self.limite_descargas,
            "estado": self.estado
        }