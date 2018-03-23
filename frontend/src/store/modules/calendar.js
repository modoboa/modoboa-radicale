import Vue from 'vue'
import * as api from '@/api'
import * as types from '../mutation-types'

// initial state
const state = {
    calendars: []
}

// getters
const getters = {
    calendars: state => state.calendars
}

// actions
const actions = {
    getCalendars ({ commit }) {
        return api.getUserCalendars().then(response => {
            commit(types.SET_CALENDARS, { calendars: response.data })
        })
    },
    createCalendar ({ commit }, data) {
        return api.createUserCalendar(data).then(response => {
            commit(types.ADD_CALENDAR, { calendar: response.data })
        })
    },
    updateCalendar ({ commit }, data) {
        return api.updateUserCalendar(data.pk, data).then(response => {
            commit(types.UPDATE_CALENDAR, { calendar: response.data })
        })
    },
    deleteCalendar ({ commit }, pk) {
        return api.deleteUserCalendar(pk).then(response => {
            commit(types.DELETE_CALENDAR, { pk: pk })
        })
    }
}

// mutations
const mutations = {
    [types.SET_CALENDARS] (state, { calendars }) {
        state.calendars = calendars
    },
    [types.ADD_CALENDAR] (state, { calendar }) {
        state.calendars.push(calendar)
    },
    [types.UPDATE_CALENDAR] (state, { calendar }) {
        state.calendars.filter(function (item, pos) {
            if (item.pk === calendar.pk) {
                Vue.set(state.calendars, pos, calendar)
            }
        })
    },
    [types.DELETE_CALENDAR] (state, { pk }) {
        state.calendars = state.calendars.filter(function (calendar) {
            return calendar.pk !== pk
        })
    }
}

export default {
    state,
    getters,
    actions,
    mutations
}
