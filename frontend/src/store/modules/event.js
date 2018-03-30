import * as api from '@/api'
import * as types from '../mutation-types'

// initial state
const state = {
    attendees: []
}

// getters
const getters = {
    attendees: state => state.attendees
}

// actions
const actions = {
    getAttendees ({ commit }) {
        return api.getAttendees().then(response => {
            commit(types.SET_ATTENDEES, { attendees: response.data })
        })
    }
}

// mutations
const mutations = {
    [types.SET_ATTENDEES] (state, { attendees }) {
        state.attendees = attendees
    }
}

export default {
    state,
    getters,
    actions,
    mutations
}
