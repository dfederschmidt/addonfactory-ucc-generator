import json
import logging
import sys
import traceback

import import_declare_test
from solnlib import conf_manager, log
from splunklib import modularinput as smi

ADDON_NAME = "{{cookiecutter.addon_name}}"


def logger_for_input(input_name: str) -> logging.Logger:
    normalized_input = input_name.split("/")[-1]
    return log.Logs().get_logger(
        f"{{cookiecutter.addon_name|lower}}_{normalized_input}"
    )


def get_account_api_key(session_key: str, account_name: str):
    cfm = conf_manager.ConfManager(
        session_key,
        ADDON_NAME,
        realm=f"__REST_CREDENTIAL__#{ADDON_NAME}#configs/conf-{{cookiecutter.addon_name}}_account",
    )
    account_conf_file = cfm.get_conf("{{cookiecutter.addon_name}}_account")
    return account_conf_file.get(account_name).get("username")


def get_data_from_api(logger: logging.Logger, api_key: str):
    logger.info("Getting data from an external API")
    dummy_data = [
        {
            "line1": "hello",
        },
        {
            "line2": "world",
        },
    ]
    return dummy_data


class Input(smi.Script):
    def __init__(self):
        super().__init__()

    def get_scheme(self):
        scheme = smi.Scheme("{{cookiecutter.addon_input_name}}")
        scheme.description = "{{cookiecutter.addon_input_name}} input"
        scheme.use_external_validation = True
        scheme.streaming_mode_xml = True
        scheme.use_single_instance = False
        scheme.add_argument(
            smi.Argument(
                "name", title="Name", description="Name", required_on_create=True
            )
        )
        return scheme

    def validate_input(self, definition: smi.ValidationDefinition):
        return

    def stream_events(self, inputs: smi.InputDefinition, event_writer: smi.EventWriter):
        # inputs.inputs is a Python dictionary object like:
        # {
        #   "{{cookiecutter.addon_input_name}}://<input_name>": {
        #     "account": "<account_name>",
        #     "disabled": "0",
        #     "host": "$decideOnStartup",
        #     "index": "<index_name>",
        #     "interval": "<interval_value>",
        #     "python.version": "python3",
        #   },
        # }
        for input_name, input_item in inputs.inputs.items():
            logger = logger_for_input(input_name)
            try:
                session_key = self._input_definition.metadata["session_key"]
                log_level = conf_manager.get_log_level(
                    logger=logger,
                    session_key=session_key,
                    app_name=ADDON_NAME,
                    conf_name=f"{ADDON_NAME}_settings",
                )
                logger.setLevel(log_level)
                logger.info("Start of the modular input")
                api_key = get_account_api_key(session_key, input_item.get("account"))
                data = get_data_from_api(logger, api_key)
                for line in data:
                    event_writer.write_event(
                        smi.Event(
                            data=json.dumps(line, ensure_ascii=False, default=str),
                            index=input_item.get("index"),
                            sourcetype="dummy-data",
                        )
                    )
                logger.info("End of the modular input")
            except Exception as e:
                logger.error(
                    f"Exception raised while ingesting data for "
                    f"{{cookiecutter.addon_input_name}}: {e}. Traceback: "
                    f"{traceback.format_exc()}"
                )


if __name__ == "__main__":
    exit_code = Input().run(sys.argv)
    sys.exit(exit_code)
