<template>
  <div id="app">
    <div id="leftcol" class="sidebar collapse navbar-collapse">
      <ul class="nav nav-sidebar" role="menu">
        <li class="nav-header"><translate>My calendars</translate></li>
        <li><a href="#" @click="showCalendarForm = true"><span class="fa fa-plus"></span> <translate>New calendar</translate></a></li>
        <li v-for="calendar in calendars" :key="calendar.pk" class="dropdown-submenu">
          <a href="#" @click="toggleSubmenu"><span class="square" v-bind:style="{ 'background-color': calendar.color }"></span> {{ calendar.name }}</a>
          <ul class="dropdown-menu">
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
              <a href="#" @click="deleteCalendar(calendar.pk, $event)">
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

    <notifications position="top right" group="default" />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import $ from 'jquery'
import CalendarForm from './components/CalendarForm.vue'
import CalendarAccessRulesForm from './components/CalendarAccessRulesForm.vue'

export default {
    components: {
        'calendar-form': CalendarForm,
        'calendar-accessrules-form': CalendarAccessRulesForm
    },
    computed: mapGetters([
        'calendars'
    ]),
    data () {
        return {
            currentCalendarPk: undefined,
            showCalendarForm: false,
            showAccessRulesForm: false,
            currentMenu: null
        }
    },
    created () {
        this.$store.dispatch('getCalendars')
    },
    methods: {
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
        deleteCalendar (pk, event) {
            this.closeMenu(event)
            var msg = this.$gettext('Are you sure you want to delete this calendar?')
            this.$dialog.confirm(msg).then(() => {
                this.$store.dispatch('deleteCalendar', pk).then(() => {
                    this.$bus.$emit('calendarDeleted', pk)
                    this.$notify({
                        group: 'default',
                        title: this.$gettext('Success'),
                        type: 'success',
                        text: this.$gettext('Calendar deleted')
                    })
                })
            })
        },
        closeMenu (e) {
            $(e.target).closest('ul').toggle()
            this.currentMenu = null
        },
        toggleSubmenu (e) {
            if (this.currentMenu) {
                this.currentMenu.toggle()
            }
            this.currentMenu = $(e.target).next('ul')
            this.currentMenu.toggle()
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
