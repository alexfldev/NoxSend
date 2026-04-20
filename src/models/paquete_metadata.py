from dataclasses import dataclass
from typing import Optional

@dataclass
class PaqueteMetadata:
    id: str
    tamano_bytes: int
    creado_en: str
    expira_en: str
    requiere_gan: bool = False
    gan_lat: Optional[float] = None
    gan_lng: Optional[float] = None

    def to_dict(self):
        """Convierte la DataClass a un diccionario compatible con Supabase."""
        # 1. Diccionario base solo con lo obligatorio (lo que ya tienes en tu DB)
        datos = {
            "id": self.id,
            "tamano_bytes": self.tamano_bytes,
            "creado_en": self.creado_en,
            "expira_en": self.expira_en
        }
        
        # 2. Solo si el G.A.N. está activado, inyectamos los campos extra.
        # Si no está activado, la base de datos ni se entera de que existen.
        if self.requiere_gan:
            datos["requiere_gan"] = True
            datos["gan_lat"] = self.gan_lat
            datos["gan_lng"] = self.gan_lng
            
        return datos