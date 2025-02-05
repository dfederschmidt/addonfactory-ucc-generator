import os
from contextlib import nullcontext as does_not_raise

import pytest

import tests.unit.helpers as helpers
from splunk_add_on_ucc_framework.global_config_validator import (
    GlobalConfigValidator,
    GlobalConfigValidatorException,
)
from splunk_add_on_ucc_framework import global_config as global_config_lib


def _path_to_source_dir() -> str:
    return os.path.join(
        os.getcwd(),
        "splunk_add_on_ucc_framework",
    )


@pytest.mark.parametrize(
    "filename,is_yaml",
    [
        ("valid_config.json", False),
        ("valid_config.yaml", True),
    ],
)
def test_config_validation_when_valid(filename, is_yaml):
    global_config_path = helpers.get_testdata_file_path(filename)
    global_config = global_config_lib.GlobalConfig()
    global_config.parse(global_config_path, is_yaml)
    validator = GlobalConfigValidator(_path_to_source_dir(), global_config)
    with does_not_raise():
        validator.validate()


@pytest.mark.parametrize(
    "filename,is_yaml,expectation,exception_message",
    [
        (
            "invalid_config_no_configuration_tabs.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            "[] is too short",
        ),
        (
            "invalid_config_no_name_field_in_configuration_tab_table.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            "Tab 'account' should have entity with field 'name'",
        ),
        # restHandlerName and restHandlerModule are present in the
        # "example_input_one" input
        (
            "invalid_config_both_rest_handler_name_module_are_present.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            (
                "Input 'example_input_one' has both 'restHandlerName' and "
                "'restHandlerModule' or 'restHandlerClass' fields present. "
                "Please use only 'restHandlerName' or 'restHandlerModule' "
                "and 'restHandlerClass'."
            ),
        ),
        # restHandlerName and restHandlerClass are present in the
        # "example_input_one" input
        (
            "invalid_config_both_rest_handler_name_class_are_present.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            (
                "Input 'example_input_one' has both 'restHandlerName' and "
                "'restHandlerModule' or 'restHandlerClass' fields present. "
                "Please use only 'restHandlerName' or 'restHandlerModule' "
                "and 'restHandlerClass'."
            ),
        ),
        # Only restHandlerModule is present in the "example_input_one" input
        (
            "invalid_config_only_rest_handler_module_is_present.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            (
                "Input 'example_input_one' should have both 'restHandlerModule'"
                " and 'restHandlerClass' fields present, only 1 of them was found."
            ),
        ),
        # Only restHandlerClass is present in the "example_input_one" input
        (
            "invalid_config_only_rest_handler_class_is_present.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            (
                "Input 'example_input_one' should have both 'restHandlerModule'"
                " and 'restHandlerClass' fields present, only 1 of them was found."
            ),
        ),
        (
            "invalid_config_options_missing_for_file_input.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            (
                "Options field for the file type should be present for 'service_account' field."
            ),
        ),
        (
            "invalid_config_supported_file_types_field_is_missing.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            (
                "You should define your supported file types in "
                "the `supportedFileTypes` field for the "
                "'service_account' field."
            ),
        ),
        (
            "invalid_config_configuration_string_validator_maxLength_less_than_minLength.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            (
                "Entity 'name' has incorrect string validator, "
                "'maxLength' should be greater or equal than 'minLength'."
            ),
        ),
        (
            "invalid_config_configuration_number_validator_range_should_have_2_elements.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            (
                "Entity 'interval' has incorrect number validator, "
                "it should have 2 elements under 'range' field."
            ),
        ),
        (
            "invalid_config_configuration_number_validator_range_second_element_smaller_than_first.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            (
                "Entity 'interval' has incorrect number validator, "
                "second element should be greater or equal than first element."
            ),
        ),
        (
            "invalid_config_configuration_regex_validator_non_compilable_pattern.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            (
                "Entity 'name' has incorrect regex validator, "
                "pattern provided in the 'pattern' field is not compilable."
            ),
        ),
        (
            "invalid_config_inputs_string_validator_maxLength_less_than_minLength.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            (
                "Entity 'name' has incorrect string validator, "
                "'maxLength' should be greater or equal than 'minLength'."
            ),
        ),
        (
            "invalid_config_inputs_number_validator_range_should_have_2_elements.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            (
                "Entity 'port' has incorrect number validator, "
                "it should have 2 elements under 'range' field."
            ),
        ),
        (
            "invalid_config_inputs_number_validator_range_second_element_smaller_than_first.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            (
                "Entity 'port' has incorrect number validator, "
                "second element should be greater or equal than first element."
            ),
        ),
        (
            "invalid_config_inputs_regex_validator_non_compilable_pattern.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            (
                "Entity 'name' has incorrect regex validator, "
                "pattern provided in the 'pattern' field is not compilable."
            ),
        ),
        (
            "invalid_config_no_configuration_tabs.yaml",
            True,
            pytest.raises(GlobalConfigValidatorException),
            "[] is too short",
        ),
        (
            "invalid_config_no_name_field_in_configuration_tab_table.yaml",
            True,
            pytest.raises(GlobalConfigValidatorException),
            "Tab 'account' should have entity with field 'name'",
        ),
        (
            "invalid_config_configuration_autoCompleteFields_duplicates.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            "Duplicates found for autoCompleteFields: 'Duplicate'",
        ),
        (
            "invalid_config_configuration_children_duplicates.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            "Duplicates found for autoCompleteFields children in entity 'Duplicate'",
        ),
        (
            "invalid_config_configuration_entity_duplicates.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            "Duplicates found for entity field or label",
        ),
        (
            "invalid_config_configuration_tabs_duplicates.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            "Duplicates found for tabs names or titles",
        ),
        (
            "invalid_config_inputs_services_duplicates.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            "Duplicates found for inputs (services) names or titles",
        ),
        (
            "invalid_config_inputs_entity_duplicates.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            "Duplicates found for entity field or label",
        ),
        (
            "invalid_config_inputs_children_duplicates.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            "Duplicates found for autoCompleteFields children in entity 'Single Select'",
        ),
        (
            "invalid_config_inputs_autoCompleteFields_duplicates.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            "Duplicates found for autoCompleteFields: 'Single Select'",
        ),
        (
            "invalid_config_inputs_multilevel_menu_duplicate_groups.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            "Duplicates found for multi-level menu groups' names or titles.",
        ),
        (
            "invalid_config_inputs_multilevel_menu_invalid_groupservices.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            (
                "example_input_three ServiceName in the multi-level menu does "
                "not match any services name."
            ),
        ),
        (
            "invalid_config_inputs_multilevel_menu_invalid_groupname_or_grouptitle.json",
            False,
            pytest.raises(GlobalConfigValidatorException),
            (
                "example_input_three groupName or Example Input Three "
                "groupTitle in the multi-level menu does not match any "
                "services name or title."
            ),
        ),
    ],
)
def test_config_validation_when_error(
    filename, is_yaml, expectation, exception_message
):
    global_config_path = helpers.get_testdata_file_path(filename)
    global_config = global_config_lib.GlobalConfig()
    global_config.parse(global_config_path, is_yaml)
    validator = GlobalConfigValidator(_path_to_source_dir(), global_config)
    with expectation as exc_info:
        validator.validate()
    (msg,) = exc_info.value.args
    assert msg == exception_message
