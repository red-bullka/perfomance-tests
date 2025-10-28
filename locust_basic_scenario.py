from locust import between, task, HttpUser


class BasicScenarioUser(HttpUser):
    wait_time = between(5, 15)

    @task(2)
    def get_data(self):
        self.client.get("/get")

    @task(1)
    def post_data(self):
        self.client.post("/post")

    @task(1)
    def delete_data(self):
        self.client.delete("/delete")