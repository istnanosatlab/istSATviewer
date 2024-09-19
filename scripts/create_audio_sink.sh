#!/bin/bash

# Check if the sink already exists
if pactl list sinks short | grep -q "DireWolfSink"; then
  echo "Sink 'DireWolfSink' already exists. No action taken."
else
  echo "Creating sink 'DireWolfSink'..."
  pactl load-module module-null-sink sink_name=DireWolfSink sink_properties=device.description="DireWolfSink"
fi