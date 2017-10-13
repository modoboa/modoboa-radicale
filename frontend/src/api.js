import Vue from 'vue'
import VueResource from 'vue-resource'

Vue.use(VueResource)

var userCalendarResource = Vue.resource('/api/v1/user-calendars{/pk}/')
var eventResource = Vue.resource('/api/v1/events{/pk}/')

// user-calendars API
export const getUserCalendars = (data) => {
    return userCalendarResource.get()
}

export const getUserCalendar = (pk) => {
    return userCalendarResource.get({pk: pk})
}

export const createUserCalendar = (data) => {
    return userCalendarResource.save(data)
}

// events API
export const getEvent = (pk) => {
    return eventResource.get({pk: pk})
}

export const createEvent = (data) => {
    return eventResource.save(data)
}

export const updateEvent = (pk, data) => {
    return eventResource.update({pk: pk}, data)
}

export const deleteEvent = (pk) => {
    return eventResource.delete({pk: pk})
}
