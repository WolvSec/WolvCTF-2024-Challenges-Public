#!/bin/bash

COORDS_FILE="../coords.txt"

if [ ! -f "$COORDS_FILE" ]; then
    echo "Coordinates file not found: $COORDS_FILE"
    exit 1
fi

mapfile -t coords_array < "$COORDS_FILE"

num_coords=${#coords_array[@]}

if [ "$num_coords" -eq 0 ]; then
    echo "No coordinates found in the file: $COORDS_FILE"
    exit 1
fi

# Loop through each jpg file in the folder
i=0
for file in *.jpg; do
    index=$(( i % num_coords ))
    
    current_coords=${coords_array[index]}
    IFS=',' read -r latitude longitude <<< "$current_coords"
    
    echo "Adding coordinates to $file: $latitude, $longitude"
    
    altitude=1044.854
    
    exiftool -GPSLatitude*="$latitude" -GPSLongitude*="$longitude" -GPSAltitude*="$altitude" "$file"
    
    ((i++))
done
