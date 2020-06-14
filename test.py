from scene_manager.settings.storage import StorageSettings

settings = StorageSettings(storage_dsn='redis://localhost:10000')
print(settings)
