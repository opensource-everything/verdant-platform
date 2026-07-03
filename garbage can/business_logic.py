# verdant_app/business_logic.py

import secrets
import string
import re
from datetime import datetime

# Data Dictionaries (moved from the original script)
MATERIAL_CATEGORIES = {
    'general': ['material', 'tools', 'parts', 'plants', 'trees', 'shrubs'],
    'plant': ['plants', 'trees', 'shrubs', 'flowers', 'groundcover', 'vines'],
    'hardscape': ['pavers', 'stones', 'gravel', 'mulch', 'sand', 'bricks', 'concrete', 'retaining walls', 'bricks', 'driveway pavers'],
    'soil': ['topsoil', 'compost', 'mulch', 'fertilizers', 'soil amendments', 'soil conditioners', 'peat moss'],
    'irrigation': ['sprinklers', 'drip irrigation systems', 'hoses', 'timers', 'pipes and fittings', 'valves', 'irrigation controllers'],
    'tool': ['shovels', 'rakes', 'pruners', 'wheelbarrows', 'lawn mowers', 'trimmers', 'leaf blowers', 'chainsaw', 'hedge trimmers', 'edgers'],
    'outdoor_features': ['patios', 'decks', 'pergolas', 'gazebos', 'outdoor_kitchens', 'fire pits', 'water features', 'retaining walls', 'fencing'],
    'lighting': ['landscape lighting', 'pathway lighting', 'accent lighting', 'outdoor string lights', 'deck lights'],
    'weed_control': ['herbicides', 'pesticides', 'weed barriers', 'organic control products', 'pre-emergent herbicides'],
    'lawn_care': ['grass seed', 'sod', 'lawn fertilizers', 'lawn aeration tools', 'lawn mowers', 'weed and feed products'],
    'decorative': ['statues', 'garden ornaments', 'planters', 'birdbaths', 'trellises', 'fountains'],
    'seasonal_item': ['snow removal equipment', 'de-icing products', 'salt spreaders', 'snow shovels'],
    'safety_gear': ['gloves', 'safety glasses', 'ear protection', 'work boots', 'knee pads', 'high-visibility vests']
}

SERVICES = {
    'maintenance': [
        'lawn care and mowing',
        'fertilization and weed control',
        'aeration and dethatching',
        'seasonal cleanups',
        'pruning and trimming',
        'leaf removal',
    ],
    'hardscape': [
        'landscape design consultation',
        'custom landscape design',
        'hardscape design',
        'retaining wall',
        'driveways and paving',
        'outdoor kitchen and fireplace',
        'fencing',
        'walkway',
        'deck',
        'patio',
        'outdoor lighting',
        'gazebo and arbor construction',
        'shed and storage building',
    ],
    'softscape': [
        'lawn installation and seeding',
        'flower beds and planting',
        'tree and shrub planting',
        'seasonal planting',
        'mulching and edging',
    ],
    'irrigation systems': [
        'irrigation system design',
        'irrigation system installation',
        'irrigation maintenance and repair',
    ],
    'sustainability services': [
        'xeriscaping',
        'native plant landscaping',
        'green roof and vertical gardens',
        'rain gardens',
    ],
    'outdoor structures': [
        'outdoor kitchen and fireplace',
        'gazebo and arbor construction',
        'shed and storage building',
    ],
    'water features': [
        'pond design and installation',
        'waterfall and fountain installation',
        'poolscapes',
    ],
    'snow removal': [
        'snow plowing and salting',
        'sidewalk shoveling',
    ],
    'pest control': [
        'pest and insect management',
    ],
    'consulting and education': [
        'landscape planning and budgeting',
        'sustainability consulting',
        'plant care and gardening classes',
    ],
    'lawn equipment services': [
        'lawn mower maintenance and repair',
        'power washing',
    ]
}

def generate_random_hash(length: int) -> str:
    """Generates a cryptographically secure random hexadecimal string."""
    return secrets.token_hex(length // 2)

def validate_email(email: str) -> bool:
    """Validates an email address using a regular expression."""
    email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return bool(re.search(email_regex, email))

def get_current_timestamp() -> str:
    """Returns the current timestamp in a standardized string format."""
    return datetime.now().isoformat()