import Vue from 'vue'
import VueResource from 'vue-resource'

Vue.use(VueResource)

// user-calendars API
var userCalendarResource = Vue.resource('/api/v1/user-calendars{/pk}/')

export const getUserCalendars = (data) => {
    return userCalendarResource.get()
}

export const getUserCalendar = (pk) => {
    return userCalendarResource.get({pk: pk})
}

export const createUserCalendar = (data) => {
    return userCalendarResource.save(data)
}

export const updateUserCalendar = (pk, data) => {
    return userCalendarResource.update({pk: pk}, data)
}

export const deleteUserCalendar = (pk) => {
    return userCalendarResource.delete({pk: pk})
}

// events API
var customEventActions = {
    patch: { method: 'PATCH', url: '/api/v1/user-calendars{/calendar_pk}/events{/pk}/' }
}
var eventResource = Vue.resource(
    '/api/v1/user-calendars{/calendar_pk}/events{/pk}/',
    {},
    customEventActions
)

export const getEvent = ([calendarPk, pk]) => {
    return eventResource.get({calendar_pk: calendarPk, pk: pk})
}

export const createEvent = (calendarPk, data) => {
    return eventResource.save({calendar_pk: calendarPk}, data)
}

export const updateEvent = (calendarPk, pk, data) => {
    return eventResource.update({calendar_pk: calendarPk, pk: pk}, data)
}

export const patchEvent = (calendarPk, pk, data) => {
    return eventResource.patch({calendar_pk: calendarPk, pk: pk}, data)
}

export const deleteEvent = (calendarPk, pk) => {
    return eventResource.delete({calendar_pk: calendarPk, pk: pk})
}

// attendees API
var attendeeResource = Vue.resource('/api/v1/attendees{/pk}/')

export const getAttendees = () => {
    return attendeeResource.get()
}

// mailboxes API
var mailboxResource = Vue.resource('/api/v1/mailboxes{/pk}/')

export const getMailboxes = () => {
    return mailboxResource.get()
}

// access rules API
var accessRuleResource = Vue.resource('/api/v1/accessrules{/pk}/')

export const getAccessRules = (calendarPk) => {
    var params = {}

    if (calendarPk !== undefined) {
        params.calendar = calendarPk
    }
    return accessRuleResource.get(params)
}

export const createAccessRule = (data) => {
    return accessRuleResource.save(data)
}

export const updateAccessRule = (pk, data) => {
    return accessRuleResource.update({pk: pk}, data)
}

export const deleteAccessRule = (pk) => {
    return accessRuleResource.delete({pk: pk})
}
