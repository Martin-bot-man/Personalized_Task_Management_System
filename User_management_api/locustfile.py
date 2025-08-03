from locust import HttpUser, task, between

class UserAPIUser(HttpUser):
    wait_time = between(1, 5)# wait 1-5 seconds between tasks

    @task(3)
    def get_user(self):
        self.client.get("/users/1")

    @task(1)
    def list_users(self):
        self.client.get("/users/?page=1&page_size=10")

    @task(1)
    def create_user(self):
        self.client.post("/users/", json= {"name": "Test User", "email":"test@example.com", "password":"secure123"})
