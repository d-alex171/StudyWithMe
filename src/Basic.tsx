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

export default function BasicExample() {

  const credentials = useMemo<TGetVenueMakerOptions>(
    () => ({
      mapId: "65ac2f9eca641a9a1399dc12",
      key: "65ac4f11ca641a9a1399dc36",
      secret:
        "04b0ac221ee3672ad507bf8dd23266d381ccbbd759d58ffb80680a7af3c3da36",
    }),
    []
  );

  const venue = useVenueMaker(credentials);

  const mapOptions = useMemo<TMapViewOptions>(
    () => ({
      backgroundColor: "#CFCFCF", // bg colour behind map
    }),
    []
  );

  const { elementRef, mapView } = useMapView(venue, mapOptions);

  useEffect(() => {
    if (!mapView || !venue) {
      return;
    }

    mapView.FloatingLabels.labelAllLocations();
  }, [mapView, venue]);

  return (
    <div id="app">
      <div id="ui">
        {/* render map details to ui */}
        {venue?.venue.name ?? "Loading..."}
        {venue && (
          <select
            onChange={(e) => {
              if (!mapView || !venue) {
                return;
              }

              // set floor to changed id
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
