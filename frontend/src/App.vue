<template>
  <div id="app">
    <div id="leftcol" class="sidebar collapse navbar-collapse">
      <ul class="nav nav-sidebar" role="menu">
        <li><a href="#" @click="openCreateCalendarForm"><span class="fa fa-plus"></span> <translate>New calendar</translate></a></li>
        <li class="nav-header"><translate>My calendars</translate></li>
        <li v-for="calendar in calendars" :key="calendar.pk" class="dropdown-submenu">
          <a href="#" @click="toggleSubmenu"><span class="square" v-bind:style="{ 'background-color': calendar.color }"></span> {{ calendar.name }}</a>
          <ul class="dropdown-menu">
            <li>
              <a href="#" @click="displayCalendarInfo(calendar, $event)">
                <span class="fa fa-info"></span> <translate>Information</translate>
              </a>
            </li>
            <li>
              <a href="#" @click="editCalendar(calendar, $event)">
                <span class="fa fa-edit"></span> <translate>Edit</translate>
              </a>
            </li>
            <li>
              <a href="#" @click="editCalendarAccessRules(calendar.pk, $event)">
                <span class="fa fa-filter"></span> <translate>Access rules</translate>
              </a>
            </li>
            <li>
              <a href="#" @click="deleteCalendar(calendar, $event)">
                <span class="fa fa-trash"></span> <translate>Delete</translate>
              </a>
            </li>
            <li>
              <a href="#" @click="openImportEventsForm(calendar, $event)">
                <span class="fa fa-download"></span> <translate>Import</translate>
              </a>
            </li>
          </ul>
        </li>
        <li v-if="sharedCalendars.length" class="nav-header">
          <translate>Shared calendars</translate>
        </li>
        <li v-for="calendar in sharedCalendars" :key="calendar.pk" class="dropdown-submenu">
          <a href="#" @click="toggleSharedCalendarMenu">
            <span class="square" v-bind:style="{ 'background-color': calendar.color }"></span> {{ calendar.name }}
          </a>
          <ul class="dropdown-menu">
            <li>
              <a href="#" @click="displayCalendarInfo(calendar, $event)">
                <span class="fa fa-info"></span> <translate>Information</translate>
              </a>
            </li>
            <li v-can="'modoboa_radicale.change_sharedcalendar'">
              <a href="#" @click="editCalendar(calendar, $event)">
                <span class="fa fa-edit"></span> <translate>Edit</translate>
              </a>
            </li>
            <li v-can="'modoboa_radicale.delete_sharedcalendar'">
              <a href="#" @click="deleteCalendar(calendar, $event)">
                <span class="fa fa-trash"></span> <translate>Delete</translate>
              </a>
            </li>
          </ul>
        </li>
      </ul>
    </div>
    <div class="main">
      <router-view/>
    </div>

    <calendar-form v-if="showCalendarForm" :initialCalendar="currentCalendar" :show.sync="showCalendarForm"></calendar-form>

    <calendar-accessrules-form v-if="showAccessRulesForm" :show.sync="showAccessRulesForm" :calendarPk="currentCalendarPk"></calendar-accessrules-form>

    <calendar-detail v-if="showCalendarDetail" :show.sync="showCalendarDetail" :calendar="currentCalendar"></calendar-detail>

    <import-events-form v-if="showImportEventsForm" :show.sync="showImportEventsForm" :calendar="currentCalendar">
    </import-events-form>

    <notifications position="top right" group="default" />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import $ from 'jquery'
import CalendarForm from './components/CalendarForm.vue'
import CalendarAccessRulesForm from './components/CalendarAccessRulesForm.vue'
import CalendarDetail from './components/CalendarDetail.vue'
import ImportEventsForm from './components/ImportEventsForm.vue'

export default {
    components: {
        'calendar-form': CalendarForm,
        'calendar-accessrules-form': CalendarAccessRulesForm,
        'calendar-detail': CalendarDetail,
        'import-events-form': ImportEventsForm
    },
    computed: mapGetters([
        'calendars',
        'sharedCalendars'
    ]),
    data () {
        return {
            currentCalendarPk: undefined,
            currentCalendar: undefined,
            showCalendarForm: false,
            showAccessRulesForm: false,
            showCalendarDetail: false,
            showImportEventsForm: false,
            currentMenu: null
        }
    },
    created () {
        this.$store.dispatch('getCalendars')
        this.$store.dispatch('getSharedCalendars')
    },
    methods: {
        openCreateCalendarForm () {
            this.currentCalendar = undefined
            this.showCalendarForm = true
        },
        displayCalendarInfo (calendar, event) {
            this.closeMenu(event)
            this.showCalendarDetail = true
            this.currentCalendar = calendar
        },
        editCalendar (calendar, event) {
            this.closeMenu(event)
            this.currentCalendar = calendar
            this.showCalendarForm = true
        },
        editCalendarAccessRules (pk, event) {
            this.closeMenu(event)
            this.currentCalendarPk = pk
            this.showAccessRulesForm = true
        },
        deleteCalendar (calendar, event) {
            this.closeMenu(event)
            var calType = (calendar.domain) ? 'shared' : 'user'
            var action = (calType === 'shared') ? 'deleteSharedCalendar' : 'deleteCalendar'
            var msg = this.$gettext('Are you sure you want to delete this calendar?')
            this.$dialog.confirm(msg).then(() => {
                this.$store.dispatch(action, calendar.pk).then(() => {
                    this.$bus.$emit('calendarDeleted', calendar)
                    this.$notify({
                        group: 'default',
                        title: this.$gettext('Success'),
                        type: 'success',
                        text: this.$gettext('Calendar deleted')
                    })
                })
            })
        },
        openImportEventsForm (calendar, event) {
            this.closeMenu(event)
            this.currentCalendar = calendar
            this.showImportEventsForm = true
        },
        closeMenu (e) {
            $(e.target).closest('ul').toggle()
            this.currentMenu = null
        },
      toggleSubmenu (e) {
        var newMenu = $(e.target).next('ul')
        if (this.currentMenu) {
          this.currentMenu.toggle()
          if (this.currentMenu.is(newMenu)) {
            this.currentMenu = undefined
            return
          }
        }
        this.currentMenu = newMenu
        this.currentMenu.toggle()
      },
      toggleSharedCalendarMenu (e) {
        this.toggleSubmenu(e)
      }
    }
}
</script>

<style>
 .square {
     display: inline-block;
     border-color: #ddd;
     border-radius: 1px;
     margin-right: 4px;
     height: 11px;
     width: 11px;
 }

 .dropdown-submenu {
     position: relative;
 }

 .dropdown-submenu .dropdown-menu {
     top: 0;
     left: 100%;
     margin-top: -1px;
 }
</style>
