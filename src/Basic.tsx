import {
  TGetVenueMakerOptions,
  MARKER_ANCHOR,
  COLLISION_RANKING_TIERS,
  TMapViewOptions,
} from "@mappedin/mappedin-js";
import "@mappedin/mappedin-js/lib/mappedin.css";
import { useEffect, useMemo } from "react";
import useMapClick from "./hooks/useMapClick";
import useMapView from "./hooks/useMapView";
import useVenueMaker from "./hooks/useVenueMaker";
import "./styles.css";

/* This demo shows you how to configure and render a map. */
export default function BasicExample() {
  /*
   * API keys and options for fetching the venue must be memoized
   * to prevent React from re-rendering excessively.
   */
  const credentials = useMemo<TGetVenueMakerOptions>(
    () => ({
      mapId: "65ac2f9eca641a9a1399dc12",
      key: "65ac4f11ca641a9a1399dc36",
      secret:
        "04b0ac221ee3672ad507bf8dd23266d381ccbbd759d58ffb80680a7af3c3da36",
    }),
    []
  );
  // The venue object contains all the iterable data for the map
  const venue = useVenueMaker(credentials);

  const mapOptions = useMemo<TMapViewOptions>(
    () => ({
      backgroundColor: "#CFCFCF", // Background colour behind the map
    }),
    []
  );
  // The mapView is the entrypoint to controling the map
  const { elementRef, mapView } = useMapView(venue, mapOptions);

  /* Map setup should be done in a useEffect */
  useEffect(() => {
    // Check that the map and venue were created successfully
    if (!mapView || !venue) {
      return;
    }

    // Label all spaces and desks which have a name
    mapView.FloatingLabels.labelAllLocations();
  }, [mapView, venue]);

  return (
    <div id="app">
      <div id="ui">
        {/* Render some map details to the UI */}
        {venue?.venue.name ?? "Loading..."}
        {venue && (
          <select
            onChange={(e) => {
              if (!mapView || !venue) {
                return;
              }

              // When the floor select changes we can find and set the map to that ID
              const floor = venue.maps.find((map) => map.id === e.target.value);
              if (floor) {
                mapView.setMap(floor);
              }
            }}
          >
            {/* The venue "maps" represent each floor */}
            {venue?.maps.map((level, index) => {
              return (
                <option value={level.id} key={index}>
                  {level.name}
                </option>
              );
            })}
          </select>
        )}
      </div>
      <div id="map-container" ref={elementRef}></div>
    </div>
  );
}
