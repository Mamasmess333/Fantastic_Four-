def test_food_logging_mock(monkeypatch):
    from services import db_service

    #mock save analysis function so it doesn’t need a database
    logs = []
    def mock_save_analysis(user_id, image_url, foods, rating, reason, alternative):
        logs.append({"user_id": user_id, "foods": foods})

    monkeypatch.setattr(db_service, "save_analysis", mock_save_analysis)

    #simulate logging information
    db_service.save_analysis(1, "mock_url", ["Apple"], "Healthy", "Low sugar", "Keep it up!")

    assert len(logs) == 1
    assert logs[0]["foods"] == ["Apple"]
