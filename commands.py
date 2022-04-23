
input_values = {

    "Start_input": ["start", "run organizer", "start", "organizer", "superintendent", "start superintendent", "run"],
    "Config_input": ["config", "config", "configure", "config data", "configure data", "config system",
                     "configure system", "start config", "start configuration"],
    "Diagnose_input": ["diagnose", "run diagnostics", "run diagnostic", "diagnostics", "diagnostic", 
                        "run diagnosis", "diagnosis", "diagnose", "system diagnosis", "diagnose system"],
    "Exit_input": ["exit", "exit", "leave", "terminate", "quit", "bye", "good bye", "goodbye"],
    "Help_input": ["help", "help", "commands", "show commands", "?"]
}

output_values = {
    "Start_output": ["start", "Starting Superintendent...", "Initiating organizing protocol..."],
    "Config_output": ["config", "Initiating configuration protocol...", "Starting configuration sequence..."],
    "Diagnose_output": ["diagnose", "Initiating self diagnosis...", "Starting diagnostic sequence..."],
    "Exit_output": ["exit", "Shutting system down..."],
    "Help_output": ["help", "Gathering data..."]
}


# greeting_morning_output = ["Good mornin]

input_data = [input_vals for input_vals in input_values.values()]
output_data = [output_vals for output_vals in output_values.values()]
