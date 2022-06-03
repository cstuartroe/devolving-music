import React, { Component } from "react";
import { Link } from "react-router-dom";
import { Artist_platform } from "./models";

type Platform = typeof Artist_platform[number];

type platformInfo = {
  img_link: string,
}

const platformInfo: {[k in Platform]: platformInfo} = {
  YouTube: { img_link: "https://upload.wikimedia.org/wikipedia/commons/4/4f/YouTube_social_white_squircle.svg" },
  Spotify: { img_link: "https://www.freepnglogos.com/uploads/spotify-logo-png/file-spotify-logo-png-4.png"},
  Soundcloud: { img_link: "/static/img/soundcloud.png" },
}

export default class ChoosePlatform extends Component<{}, {}> {
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
    return (
      <div className="row choose-platform">
        <div className="col-12" style={{paddingBottom: "4vh"}}>
          <h2>
            You may submit a playlist on any of these platforms:
          </h2>
        </div>

        {Artist_platform.map(this.platformTile)}
      </div>
    );
  }
}
