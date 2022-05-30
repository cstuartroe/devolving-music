import React, { Component } from "react";
import { Link } from "react-router-dom";

export default class SubmitPlaylist extends Component<{}, {}> {
  platformTile(name: string, path: string, img_link: string) {
    return (
      <div className="col-12 col-md-4 platform-tile" style={{
        backgroundImage: `url("${img_link}")`
      }}>
        <Link to={`/submit-playlist/${path}`}>
          {name}
        </Link>
      </div>
    );
  }

  render() {
    return (
      <div className="row submit-playlist">
        <div className="col-12" style={{paddingBottom: "4vh"}}>
          <h2>
            You may submit a playlist on any of these platforms:
          </h2>
        </div>

        {this.platformTile(
          "Youtube",
          "youtube",
          "https://upload.wikimedia.org/wikipedia/commons/4/4f/YouTube_social_white_squircle.svg",
        )}
        {this.platformTile(
          "Spotify",
          "spotify",
          "https://www.freepnglogos.com/uploads/spotify-logo-png/file-spotify-logo-png-4.png",
        )}
        {this.platformTile(
          "Soundcloud",
          "soundcloud",
          "/static/img/soundcloud.png",
        )}
      </div>
    );
  }
}
