
resource "google_cloud_run_v2_service" "default" {
  project  = "bitespeed-interview-project"
  provider = google-beta
  name     = "app"
  location = "us-central1"
  launch_stage = "BETA"
  ingress = "INGRESS_TRAFFIC_ALL"
  template {
    scaling {
      max_instance_count = 1
    }

    containers {
      name = "app"
      ports {
        container_port = 80
      }
      image = "gcr.io/bitespeed-interview-project/app"
    }
  }
  

  lifecycle {
    ignore_changes = [
      launch_stage,
    ]
  }
}

data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location    = google_cloud_run_v2_service.default.location
  project     = google_cloud_run_v2_service.default.project
  service     = google_cloud_run_v2_service.default.name

  policy_data = data.google_iam_policy.noauth.policy_data
}

output "url" {
  value = google_cloud_run_v2_service.default.uri
}