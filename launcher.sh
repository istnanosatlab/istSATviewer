# Define the config file
CONFIG_FILE="config"


# Function to read parameters from the config file
get_config_value() {
    grep "$1" "$CONFIG_FILE" | awk -F': ' '{print $2}'

}

# Read gnu radio parameters
SCRIPT=$(get_config_value "gnuradio_script")
RX_OFFSET=$(get_config_value "rx_offset")
GAIN=$(get_config_value "gain")



# Read satviewer params
GS_CALLSIGN=$(get_config_value "gs-callsign")
SC_CALLSIGN=$(get_config_value "sc-callsign")
GR_ADDRESS=$(get_config_value "gr-address")
GR_PORT=$(get_config_value "gr-port")
MOD_CTRL_PORT=$(get_config_value "modulation-controller-port")
CSV_FOLDER=$(get_config_value "csv-folder")





# Launch the gnu radio program with the parameters
gnuradio_command="python3 $SCRIPT > /dev/null &"
echo "Launching gnu radio command: $gnuradio_command"
eval $gnuradio_command



# Launch the satviewer program with the parameters
satviewer_command="./satExec3_10 --gs-callsign $GS_CALLSIGN --sc-callsign $SC_CALLSIGN --gr-address $GR_ADDRESS --gr-port $GR_PORT --modulation-controller-port $MOD_CTRL_PORT --csv-folder $CSV_FOLDER"
echo "Launching satviewer command: $satviewer_command"
eval $satviewer_command

