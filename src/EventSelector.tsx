import React, { Component } from "react";
import ResourceManager from "./ResourceManager";
import { Event } from "./models";


export type event_setter = (e: Event) => void;

type EventSelectorProps = {
  setEvent: event_setter,
}

type EventSelectorState = {
  events?: Event[],
}

export default class EventSelector extends Component<EventSelectorProps, EventSelectorState>{
  constructor(props: EventSelectorProps) {
    super(props);

    this.state = {}
  }

  componentDidMount() {
    ResourceManager.getModels("events").then(events => this.setState({events}));
  }

  render() {
    if (this.state.events === undefined) {
      return null;
    } else {
      return (
        <div>
          {this.state.events.map(event => (
            <div key={event.id}>{event.name}</div>
          ))}
        </div>
      );
    }
  }
}
