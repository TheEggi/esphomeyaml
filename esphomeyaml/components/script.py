import voluptuous as vol

from esphomeyaml import automation
from esphomeyaml.automation import ACTION_REGISTRY, maybe_simple_id
import esphomeyaml.config_validation as cv
from esphomeyaml.const import CONF_ID
from esphomeyaml.cpp_generator import Pvariable, get_variable
from esphomeyaml.cpp_types import Action, NoArg, Trigger, esphomelib_ns

Script = esphomelib_ns.class_('Script', Trigger.template(NoArg))
ScriptExecuteAction = esphomelib_ns.class_('ScriptExecuteAction', Action)
ScriptStopAction = esphomelib_ns.class_('ScriptStopAction', Action)

CONFIG_SCHEMA = automation.validate_automation({
    vol.Required(CONF_ID): cv.declare_variable_id(Script),
})


def to_code(config):
    for conf in config:
        trigger = Pvariable(conf[CONF_ID], Script.new())
        automation.build_automation(trigger, NoArg, conf)


CONF_SCRIPT_EXECUTE = 'script.execute'
SCRIPT_EXECUTE_ACTION_SCHEMA = maybe_simple_id({
    vol.Required(CONF_ID): cv.use_variable_id(Script),
})


@ACTION_REGISTRY.register(CONF_SCRIPT_EXECUTE, SCRIPT_EXECUTE_ACTION_SCHEMA)
def script_execute_action_to_code(config, action_id, arg_type, template_arg):
    for var in get_variable(config[CONF_ID]):
        yield None
    rhs = var.make_execute_action(template_arg)
    type = ScriptExecuteAction.template(arg_type)
    yield Pvariable(action_id, rhs, type=type)


CONF_SCRIPT_STOP = 'script.stop'
SCRIPT_STOP_ACTION_SCHEMA = maybe_simple_id({
    vol.Required(CONF_ID): cv.use_variable_id(Script),
})


@ACTION_REGISTRY.register(CONF_SCRIPT_STOP, SCRIPT_STOP_ACTION_SCHEMA)
def script_stop_action_to_code(config, action_id, arg_type, template_arg):
    for var in get_variable(config[CONF_ID]):
        yield None
    rhs = var.make_stop_action(template_arg)
    type = ScriptStopAction.template(arg_type)
    yield Pvariable(action_id, rhs, type=type)
