import Vue from 'vue'
import VueResource from 'vue-resource'

Vue.use(VueResource)

// user-calendars API
var userCalendarResource = Vue.resource('/api/v1/user-calendars{/pk}/')

export const getUserCalendars = (data) => {
    return userCalendarResource.get()
}

export const getUserCalendar = (pk) => {
    return userCalendarResource.get({ pk: pk })
}

export const createUserCalendar = (data) => {
    return userCalendarResource.save(data)
}

export const updateUserCalendar = (pk, data) => {
    return userCalendarResource.update({ pk: pk }, data)
}

export const deleteUserCalendar = (pk) => {
    return userCalendarResource.delete({ pk: pk })
}

// shared calendars API
var sharedCalendarResource = Vue.resource('/api/v1/shared-calendars{/pk}/')

export const getSharedCalendars = () => {
    return sharedCalendarResource.get()
}

export const getSharedCalendar = (pk) => {
    return sharedCalendarResource.get({ pk: pk })
}

export const createSharedCalendar = (data) => {
    return sharedCalendarResource.save(data)
}

export const updateSharedCalendar = (pk, data) => {
    return sharedCalendarResource.update({ pk: pk }, data)
}

export const deleteSharedCalendar = (pk) => {
    return sharedCalendarResource.delete({ pk: pk })
}

// events API
var customEventActions = {
    patch: { method: 'PATCH', url: '/api/v1{/type}-calendars{/calendar_pk}/events{/pk}/' },
    importEvents: { method: 'POST', url: '/api/v1{/type}-calendars{/calendar_pk}/events/import_from_file/' }
}
var eventResource = Vue.resource(
    '/api/v1{/type}-calendars{/calendar_pk}/events{/pk}/',
    {},
    customEventActions
)

export const getEvent = (calendarPk, calendarType, pk) => {
    return eventResource.get({ type: calendarType, calendar_pk: calendarPk, pk: pk })
}

export const createEvent = (calendar, data) => {
    var type = (calendar.domain) ? 'shared' : 'user'
    return eventResource.save({ type: type, calendar_pk: calendar.pk }, data)
}

export const updateEvent = (calendar, pk, data) => {
    var newCalType = (data.calendar.domain) ? 'shared' : 'user'
    if (newCalType !== calendar.type) {
        data['new_calendar_type'] = newCalType // eslint-disable-line dot-notation
    }
    data.calendar = data.calendar.pk
    return eventResource.update({
        type: calendar.type, calendar_pk: calendar.pk, pk: pk
    }, data)
}

export const patchEvent = (calendar, pk, data) => {
    var type = (calendar.domain) ? 'shared' : 'user'
    return eventResource.patch({ type: type, calendar_pk: calendar.pk, pk: pk }, data)
}

export const deleteEvent = (calendar, pk) => {
    var type = (calendar.domain) ? 'shared' : 'user'
    return eventResource.delete({ type: type, calendar_pk: calendar.pk, pk: pk })
}

export const importEvents = (calendar, data) => {
    var type = (calendar.domain) ? 'shared' : 'user'
    return eventResource.importEvents({ type: type, calendar_pk: calendar.pk }, data)
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

// domains API
var domainResource = Vue.resource('/api/v1/domains{/pk}/')

export const getDomains = () => {
    return domainResource.get()
}

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
    return accessRuleResource.update({ pk: pk }, data)
}

export const deleteAccessRule = (pk) => {
    return accessRuleResource.delete({ pk: pk })
}
