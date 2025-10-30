assets = {}

def load_asset(name, data):
    """Add or replace an asset"""
    assets[name] = data
    print(f"[ASSET] ✅ Loaded '{name}'")

def get_asset(name):
    """Fetch an asset"""
    return assets.get(name, None)

def unload_asset(name):
    """Remove an asset"""
    if name in assets:
        del assets[name]
        print(f"[ASSET] 🧹 Unloaded '{name}'")
    else:
        print(f"[ASSET] ⚠️ Asset '{name}' not found")

def list_assets():
    """List all loaded assets"""
    if not assets:
        print("[ASSET] 💤 No assets loaded")
        return
    print("[ASSET] 📦 Loaded assets:")
    for name in assets:
        print(f" - {name}")
