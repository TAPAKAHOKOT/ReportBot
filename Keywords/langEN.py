class Keywords:
    def __init__(self):
        # ! Commands
        # * /Start
        self.start = ["Running main keyboard", 
        "Configure your UTC settings or all the time will be displayed by UTC+3"]
        
        # * /Settings
        self.settings = "Select the setting you want"

        # * /help
        self.help = ["??Hi there, using this bot you can count your working or studying time??\n"]
        self.help[0] += "Try it? (touch 'Start working' button)\n\n"
        self.help[0] += "At any time you can change yor status from working to stutying and vice versa??\n"
        self.help[0] += "To do it, touch 'Status/Tag' button\n\n"
        self.help[0] += "Also you can get hours worked reports, otouch 'Work reports'??\n\n"
        self.help[0] += "After all, you can easily add/delete/edit hours worked manually?? (touch 'Actions with periods')"

        # ! Command messages
        # * main
        self.main = "Openning main keyboard"

        # * Work reports
        self.work_reports = "Choose worked time report period"

        # * Start Working >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        self.start_working = ["You are already working from {} {}",
                        "Start working time: "]
        
        # * Stop Working >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        self.stop_working = ["You aren't working now",
                            "End working time: {}\nWorking time: {}"]
        
        # * Tags
        self.tags = "Tag changed to: "

        # * Status/Tag
        self.status_tag = "Click to change"

        # * Change tag
        self.change_tag = ["\n\nChoose a tag or write your tag in chat\n(# + tag name)",
                            "\nback",
                            "\nTag changed to "]
        
        # * Change status
        self.change_status = ["\nStatus changed to 'Studying'",
                                "\nStatus changed to 'Working'"]

        # * Worked reports >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # * UTC Change menu
        self.utc_change_menu = "Configure your UTC settings or all the time will be displayed by UTC+3"

