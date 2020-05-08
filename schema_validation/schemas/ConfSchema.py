from schema import Schema, And, Use

mqtt_iface_conf_schema = Schema({
    "host": And(Use(str)),
    "port": And(Use(int)),
    "timeout": And(Use(int)),
    "subscribe": And(Use(list))
})

kernel_conf_schema = Schema({
    "component_name": And(Use(str)),
    "comm_iface": mqtt_iface_conf_schema
})
