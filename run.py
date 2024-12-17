from app import create_app

if __name__ == '__main__':
    app = create_app(__name__, 'postgresql://movies_api_db_tutorial_user:gUQPbDaUWlpCluIayBxWP29JhCIAEpLM@dpg-ctgoeijgbbvc738te8j0-a.oregon-postgres.render.com/movies_api_db_tutorial', True)
    app.run()