/**
 * @file app/src/router.js
 *
 * This is the main routes file for the application.
 */
import Vue from 'vue'
import Router from 'vue-router'

import Home from './views/Home.vue';
import Auth from './views/Auth.vue';
import Admin from './views/Admin.vue';

import Employee from './views/Employee.vue';
import EmployeeTimesheet from './views/EmployeeTimesheet.vue';
import EmployeeContract from './views/EmployeeContract.vue';

import Group from './views/Group.vue';
import Activity from './views/Activity.vue';

Vue.use(Router);

const router = new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        // home
        // this page renders the default page
        {
            path: '/',
            name: 'home',
            component: Home,
        },
        // auth
        // this page renders the authentication steps in the application
        {
            path: '/auth',
            name: 'auth',
            component: Auth,
        },
        // admin
        // this page renders the admin view
        {
            path: '/admin',
            name: 'admin',
            component: Admin,
            props: (route) => ({ initial_tab: route.query.tab })
        },
        // employee
        // this page renders the (admin) employee view
        {
            path: '/employees/:employee_id',
            name: 'employee',
            component: Employee,
            props: (route) => ({ initial_tab: route.query.tab , employee_id: route.params.employee_id})
        },
        // employee - timesheet
        // this page renders the (admin) employee - timesheet view
        {
            path: '/employees/:employee_id/timesheets/:date',
            name: 'employee-timesheet',
            component: EmployeeTimesheet,
            props: true,
        },
        // employee - contract
        // this page renders the (admin) employee - contract view
        {
            path: '/employees/:employee_id/contracts/:start_date',
            name: 'employee-contract',
            component: EmployeeContract,
            props: true,
        },
        // group
        // this page renders the (admin) group view
        {
            path: '/groups/:group_id',
            name: 'group',
            component: Group,
            props: true,
        },
        // activity
        // this page renders the (admin) activity view
        {
            path: '/activities/:activity_id',
            name: 'activity',
            component: Activity,
            props: true
        }
    ]
});

export default router;


