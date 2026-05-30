import pygame

def load_and_crop(path, scale_factor=3):
    """Load an image, crop transparent borders, then scale once.

    Returns a Surface (never None) - on failure returns a visible placeholder.
    """
    try:
        img = pygame.image.load(path).convert_alpha()
    except Exception as e:
        print(f"Failed to load {path}: {e}")
        img = None

    if img:
        try:
            bbox = img.get_bounding_rect()
            if bbox.width == 0 or bbox.height == 0:
                print(f"Image {path} appears empty after bounding box test.")
            else:
                img = img.subsurface(bbox).copy()
        except Exception as e:
            print(f"Error cropping {path}: {e}")

        try:
            img = pygame.transform.scale(img, (img.get_width() * scale_factor, img.get_height() * scale_factor))
        except Exception as e:
            print(f"Scaling error for {path}: {e}")
            # fall through to placeholder creation

    if not img:
        # create visible placeholder
        ph = pygame.Surface((32 * scale_factor, 32 * scale_factor), pygame.SRCALPHA)
        ph.fill((200, 0, 200, 255))
        pygame.draw.rect(ph, (0,0,0), ph.get_rect(), 2)
        return ph

    return img
