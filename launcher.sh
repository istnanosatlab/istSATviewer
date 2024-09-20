# Define the config file
CONFIG_FILE="config"


# Function to read parameters from the config file
get_config_value() {
    grep "$1" "$CONFIG_FILE" | awk -F': ' '{print $2}'
}

# Function to add a prefix to the parameter
add_prefix() {
    VALUE=$(get_config_value "$1")
    if [ -n "$VALUE" ]; then  # Check if VALUE is not empty
        echo "--$1 $VALUE"
    fi
}

# Read gnu radio parameters
SCRIPT=$(get_config_value "gnuradio_script")
SERIAL_PORT=$(add_prefix "serial-port")
BAUD_RATE=$(add_prefix "baud-rate")
RX_OFFSET=$(add_prefix "rx-offset")
GAIN=$(add_prefix "gain")


# Read satviewer params
GS_CALLSIGN=$(add_prefix "gs-callsign")
SC_CALLSIGN=$(add_prefix "sc-callsign")
GR_ADDRESS=$(add_prefix "gr-address")
GR_PORT=$(add_prefix "gr-port")
MOD_CTRL_PORT=$(add_prefix "modulation-controller-port")
CSV_FOLDER=$(add_prefix "csv-folder")


# Launch the gnu radio program with the parameters
gnuradio_command="python3 $SCRIPT $SERIAL_PORT $BAUD_RATE > /dev/null &"
echo "Launching gnu radio command: $gnuradio_command"
eval $gnuradio_command

# wait five seconds
sleep 5


# Launch the satviewer program with the parameters
satviewer_command="./satExec3_10 $GS_CALLSIGN $SC_CALLSIGN $GR_ADDRESS $GR_PORT $MOD_CTRL_PORT $CSV_FOLDER &"
echo "Launching satviewer command: $satviewer_command"
eval $satviewer_command

#wait five seconds
sleep 5


# Launch smoothviewer to view the data in the browser
smoothviewer_command="python3 smoothviewer/app.py"
echo "Launching smoothviewer"
eval $smoothviewer_command

