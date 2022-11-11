require "rest-client"
require "json"
RestClient.post "https://platan.us/recruiting/job-application", {"name":"Felipe Neira Osses","email":"fneiraosses.97@gmail.com","github": "https://github.com/felipeneira","job_code": "D09F56843B2A42549087F2D9CCA54411"}.to_json, :content_type => "application/json"