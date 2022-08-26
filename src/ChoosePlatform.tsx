import React, { Component } from "react";
import { Link, Navigate } from "react-router-dom";
import { Event, Artist_platform } from "./models";

type Platform = typeof Artist_platform[number];

type Allowance = "allow_spotify" | "allow_youtube" | "allow_soundcloud";

const platformAllowances: {[key in Platform]: Allowance} = {
  "Spotify": "allow_spotify",
  "YouTube": "allow_youtube",
  "Soundcloud": "allow_soundcloud",
}


type platformInfo = {
  img_link: string,
}

const platformInfo: {[k in Platform]: platformInfo} = {
  YouTube: { img_link: "https://upload.wikimedia.org/wikipedia/commons/4/4f/YouTube_social_white_squircle.svg" },
  Spotify: { img_link: "https://www.freepnglogos.com/uploads/spotify-logo-png/file-spotify-logo-png-4.png"},
  Soundcloud: { img_link: "/static/img/soundcloud.png" },
}

export const getAllowedPlatforms = (event: Event) => (
  Artist_platform.filter(platform => event[platformAllowances[platform]]))

type Props = {
  event: Event,
}

export default class ChoosePlatform extends Component<Props, {}> {
  platformTile(platform: Platform) {
    return (
      <div className="col-12 col-md-4 platform-tile" key={platform} style={{
        backgroundImage: `url("${platformInfo[platform].img_link}")`
      }}>
        <Link to={`/submit-playlist/${platform}`} className="center">
          {platform}
        </Link>
      </div>
    );
  }

  render() {
    const allowed_platforms = getAllowedPlatforms(this.props.event);

    if (allowed_platforms.length == 1) {
      return <Navigate to={`/submit-playlist/${allowed_platforms[0]}`}/>;
    }

    return (
      <div className="row choose-platform">
        <div className="col-12" style={{paddingBottom: "4vh"}}>
          <h2>
            You may submit a playlist on any of these platforms:
          </h2>
        </div>

        {allowed_platforms.map(this.platformTile)}
      </div>
    );
  }
}
