from dataclasses import dataclass

@dataclass
class PaqueteMetadata:
    """
    Esto es básicamente una 'plantilla' o 'molde'. 
    Sirve para asegurarme de que a la base de datos de Supabase solo se envía 
    esta información pública. Fíjate que NO guardamos ni contraseñas ni nombres de archivo.
    """
    id: str
    tamano_bytes: int
    creado_en: str
    expira_en: str
    descargas_actuales: int = 0
    limite_descargas: int = 1
    estado: str = "activo"

    def to_dict(self) -> dict:
        """Convierte este molde en un diccionario normal para que Supabase lo entienda al subirlo."""
        return {
            "id": self.id,
            "tamano_bytes": self.tamano_bytes,
            "creado_en": self.creado_en,
            "expira_en": self.expira_en,
            "descargas_actuales": self.descargas_actuales,
            "limite_descargas": self.limite_descargas,
            "estado": self.estado
        }