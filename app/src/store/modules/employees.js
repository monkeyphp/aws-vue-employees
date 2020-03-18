/**
 * @file app/src/store/modules/employees.js
 *
 * This file provides a Vuex module definition for interacting with the `employees` api.
 */
import Vue from 'vue'
import employees from '../../api/employees'

/* eslint-disable */

/**
 * @type {{employees: Array}}
 */
const state = {
    // array of Employees
    employees: [],

    // array of Employee Timesheets
    employee_timesheets: [],

    // array of Employee Timesheet Entries
    employee_timesheet_entries: [],

    // array of Employee Contracts
    employee_contracts: [],
};

/**
 * @type {{get_employee(*=, *=): Promise<any>, get_employees(*=): Promise<any>, post_employee_timesheet(*=, *=): *, post_employee_contract(*=, *=): Promise<any>, post_employee(*=, *=): Promise<any>, get_employee_contracts(*=, *=): Promise<any>, get_employee_timesheets(*=, *=): *}}
 */
const actions = {
    /**
     * Return a list of all Employees
     *
     * @param context
     * @returns {Promise<any>}
     */
    get_employees (context, parent_group_id=null) {
        return new Promise((resolve, reject) => {
            employees.employees_get(parent_group_id)
                .then((response) => {
                    response.forEach((employee) => {
                        context.commit('ADD_EMPLOYEE', employee)
                    });
                    resolve();
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },

    /**
     * Return a list of Employees that have been added to the specified Group.
     *
     * @param context
     * @param group_id
     * @returns {Promise<any>}
     */
    // get_group_employees (context, group_id) {
    //     return new Promise((resolve, reject) => {
    //         employees.group_employees_get(group_id)
    //             .then((response) => {
    //                 response.forEach( (employee) => {
    //                     context.commit('ADD_EMPLOYEE', employee);
    //                 });
    //                 resolve();
    //             })
    //             .catch((error) => {
    //                 reject(error);
    //             })
    //     });
    // },

    /**
     * Create an Employee
     *
     * @param context
     * @param employee
     * @returns {Promise<any>}
     */
    post_employee (context, employee) {
        return new Promise((resolve, reject) => {
            employees.employees_post(employee)
                .then((employee) => {
                    context.commit('ADD_EMPLOYEE', employee);
                    resolve();
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },

    /**
     * Return the Employee identified by the supplied employee_id
     *
     * @param context
     * @param employee_id
     * @returns {Promise<any>}
     */
    get_employee (context, employee_id) {
        return new Promise((resolve, reject) => {
            employees.employee_get(employee_id)
                .then((employee) => {
                    context.commit('ADD_EMPLOYEE', employee);
                    resolve();
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    /**
     * Put (update) an Employee record
     *
     * @param context
     * @param employee
     * @returns {Promise<any>}
     */
    put_employee (context, employee) {
        return new Promise((resolve, reject) => {
            employees.employee_put(employee)
                .then((employee) => {
                    context.commit('ADD_EMPLOYEE', employee);
                    resolve();
                })
                .catch((error) => {
                    reject(error);
                })
        });
    },
    /**
     * Delete the specified Employee
     *
     * @param context
     * @param employee
     * @returns {Promise<any>}
     */
    delete_employee (context, employee) {
        return new Promise((resolve, reject) => {
            const employee_id = employee.employee_id;
            employees.employee_delete(employee_id)
                .then(() => {
                    context.commit('REMOVE_EMPLOYEE', employee);

                    // probably quite inefficient
                    const employee_contracts = context.state.employee_contracts.filter((employee_contract) => employee_contract.employee_id === employee_id );
                    employee_contracts.forEach((employee_contract) => {
                        context.commit('REMOVE_EMPLOYEE_CONTRACT', employee_contract)
                    });

                    // probably quite inefficient
                    const employee_timesheets = context.state.employee_timesheets.filter((employee_timesheet) => employee_timesheet.employee_id === employee_id );
                    employee_timesheets.forEach((employee_timesheet) => {
                        context.commit('REMOVE_EMPLOYEE_TIMESHEET', employee_timesheet)
                    });

                    resolve();
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },

    /**
     * Return a list of Timesheets that belong to the Employee specified by the supplied employee_id
     *
     * @param context
     * @param employee_id
     * @returns {Promise<any>}
     */
    get_employee_timesheets (context, employee_id) {
        return new Promise((resolve, reject) => {
            employees.employee_timesheets_get(employee_id)
                .then((response) => {
                    response.forEach((employee_timesheet) => {
                        context.commit('ADD_EMPLOYEE_TIMESHEET', employee_timesheet);
                    });
                    resolve();
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },

    get_employee_timesheet (context, {employee_id, date}) {
        return new Promise((resolve, reject) => {
            employees.employee_timesheet_get(employee_id, date)
                .then((timesheet) => {
                    context.commit('ADD_EMPLOYEE_TIMESHEET', timesheet);
                    resolve();
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },

    /**
     * Delete the Timesheet specified by the supplied employee and date.
     *
     * @param context
     * @param employee_id
     * @param date
     * @returns {Promise<any>}
     */
    delete_employee_timesheet(context, {employee_id, date}) {
        return new Promise((resolve, reject) => {

        });
    },

    get_employee_timesheet_entries (context, {employee_id, date}) {
        return new Promise((resolve, reject) => {
            employees.employee_timesheet_entries_get(employee_id, date)
                .then((response) => {
                    response.forEach((entry) => {
                        context.commit('ADD_EMPLOYEE_TIMESHEET_ENTRY', entry);
                    });
                    resolve();
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },

    /**
     * Post an Entry.
     *
     * @param context
     * @param entry
     * @returns {Promise<any>}
     */
    post_employee_timesheet_entry (context, entry) {
        const employee_id = entry['employee_id'];
        const date = entry['date'];

        return new Promise((resolve, reject) => {
            employees.employee_timesheet_entries_post(employee_id, entry)
                .then((entry) => {
                    context.commit('ADD_EMPLOYEE_TIMESHEET_ENTRY', entry);

                    context.dispatch('get_employee_timesheet', {employee_id: employee_id, date: date});
                    resolve();
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },

    get_employee_timesheet_entry (context, {employee_id, date, time}) {
        return new Promise((resolve, reject) => {
            employees.employee_timesheet_entry_get(employee_id, date, time)
                .then((entry) => {
                    context.commit('ADD_EMPLOYEE_TIMESHEET_ENTRY', entry);
                    resolve();
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    /**
     * Delete the specified Timesheet Entry.
     *
     * @param context
     * @param entry
     * @returns {Promise<any>}
     */
    delete_employee_timesheet_entry (context, entry) {
        const employee_id = entry['employee_id'];
        const date = entry['date'];

        return new Promise((resolve, reject) => {
            employees.employee_timesheet_entry_delete(employee_id, date)
                .then(() => {
                    context.commit('REMOVE_EMPLOYEE_TIMESHEET_ENTRY', entry);
                    context.dispatch('get_employee_timesheet', {employee_id: employee_id, date: date});
                    resolve();
                }).catch((error) => {
                    reject(error);
                });
        });
    },

    // put_employee_timesheet_entry (context, entry) {
    //
    // },

    // delete_employee_time_entry (context, {employee_id, date, time}) {
    //
    // },

    /**
     * Return the Contracts for the Employee specified by the supplied employee_id
     *
     * @param context
     * @param employee_id
     * @returns {Promise<any>}
     */
    get_employee_contracts(context, employee_id) {
        return new Promise((resolve, reject) => {
            employees.employee_contracts_get(employee_id)
                .then((response) => {
                    response.forEach((contract) => {
                        context.commit('ADD_EMPLOYEE_CONTRACT', contract);
                    });
                    resolve();
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    /**
     * Post a Contract
     *
     * @param context
     * @param employee_contract
     * @returns {Promise<any>}
     */
    post_employee_contract(context, employee_contract) {
        const employee_id = employee_contract['employee_id'];
        return new Promise((resolve, reject) => {
            employees.employee_contracts_post(employee_id, employee_contract)
                .then((employee_contract) => {
                    context.commit('ADD_EMPLOYEE_CONTRACT', employee_contract);
                    resolve();
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },

    /**
     * Return the Employee Contract identified by the supplied employee_id and start_date
     *
     * @param context
     * @param employee_id
     * @param start_date
     */
    get_employee_contract (context, {employee_id, start_date}) {
        return new Promise((resolve, reject) => {
            employees.employee_contract_get(employee_id, start_date)
                .then((employee_contract) => {
                    context.commit('ADD_EMPLOYEE_CONTRACT', employee_contract);
                    resolve();
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },

    // delete_employee_contract  (context, {employee_id, date}) {
    //
    // },

    /**
     * Put a Contract
     *
     * @param context
     * @param contract
     * @returns {Promise<any>}
     */
    put_employee_contract(context, contract) {
        const employee_id = contract['employee_id'];
        const start_date = contract['start_date'];
        return new Promise((resolve, reject) => {
            employees.employee_contract_put(employee_id, start_date, contract)
                .then((contract) => {
                    context.commit('ADD_EMPLOYEE_CONTRACT', contract);
                    resolve();
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
};



const mutations = {
    /**
     * Add an Employee record to the state
     *
     * @param state
     * @param employee
     * @constructor
     */
    ADD_EMPLOYEE (state, employee) {
        const employee_id = employee.employee_id;
        const index = state.employees.findIndex((employee) => employee.employee_id === employee_id);

        if (employee.hasOwnProperty('created')) {
            let created = employee.created;
            employee['created'] = new Date(Date.parse(created)).toLocaleDateString('en-GB', {dateStyle: 'medium', timeStyle: 'medium'});
        }

        if (employee.hasOwnProperty('name')) {
            let name = employee.name;
            let initials = name.match(/\b\w/g).join('');

            let colors = [
                'pink',
                'purple',
                'deep-purple',
                'blue',
                'light-blue',
                'cyan',
                'teal',
                'green',
                'light-green',
                'lime',
                'yellow',
                'amber',
                'orange',
                'deep-orange',
                'blue-grey'
            ];
            // @link https://stackoverflow.com/questions/4550505/getting-a-random-value-from-a-javascript-array
            let color = colors[Math.floor(Math.random() * colors.length)];

            employee['color'] = color;
            employee['initials'] = initials;
        }

        if (index >= 0) {
            Vue.set(state.employees, index, employee);
        } else {
            state.employees.push(employee);
        }
    },

    /**
     * Remove the Employee identified by the supplied employee object
     *
     * @param state
     * @param employee
     * @constructor
     */
    REMOVE_EMPLOYEE (state, employee) {
        const employee_id = employee.employee_id;
        const index = state.employees.findIndex((employee) => employee.employee_id === employee_id);

        if (index >= 0) {
            state.employees.splice(index, 1)
        }
    },

    /**
     * Add a Contract record to the state
     *
     * @param state
     * @param contract
     * @constructor
     */
    ADD_EMPLOYEE_CONTRACT (state, contract) {
        const start_date = contract.start_date;
        const index = state.employee_contracts.findIndex((employee_contract) => employee_contract.start_date === start_date);

        if (contract.hasOwnProperty('created')) {
            let created = contract.created;
            contract['created'] = new Date(Date.parse(created)).toLocaleDateString('en-GB', {dateStyle: 'medium', timeStyle: 'medium'});
        }
        if (index >= 0) {
            Vue.set(state.employee_contracts, index, contract);
        } else {
            state.employee_contracts.push(contract);
        }
    },
    /**
     * Remove the supplied Contract from the state
     *
     * @param state
     * @param contract
     * @constructor
     */
    REMOVE_EMPLOYEE_CONTRACT (state, contract) {
        const employee_id = contract.employee_id;
        const contract_id = contract.contract_id;

        const index = state.employee_contracts.findIndex((employee_contract) => employee_contract.contract_id === contract_id && employee_contract.employee_id === employee_id);

        if (index >= 0) {
            state.employee_contracts.splice(index, 1)
        }
    },

    /**
     * Add a Timesheet record to the state
     *
     * @param state
     * @param employee_timesheet
     * @constructor
     */
    ADD_EMPLOYEE_TIMESHEET (state, employee_timesheet) {
        const employee_id = employee_timesheet.employee_id;
        const date = employee_timesheet.date;

        const index = state.employee_timesheets.findIndex((employee_timesheet) =>
            employee_timesheet.employee_id === employee_id &&
            employee_timesheet.date === date
        );

        if (employee_timesheet.hasOwnProperty('created')) {
            let created = employee_timesheet.created;
            employee_timesheet['created'] = new Date(Date.parse(created)).toLocaleDateString('en-GB', {dateStyle: 'medium', timeStyle: 'medium'});
        }

        let d = new Date(Date.parse(date));
        const month = new Intl.DateTimeFormat('en-GB', {  month: 'long'}).format(d);
        const year = new Intl.DateTimeFormat('en-GB', {  year: 'numeric',}).format(d);
        const day = new Intl.DateTimeFormat('en-GB', { day: '2-digit'}).format(d);
        const weekday = new Intl.DateTimeFormat('en-GB', { weekday: 'long'}).format(d);

        employee_timesheet['month'] = month;
        employee_timesheet['year'] = year;
        employee_timesheet['day'] = day;
        employee_timesheet['weekday'] = weekday;

        if (index >= 0) {
            Vue.set(state.employee_timesheets, index, employee_timesheet);
        } else {
            state.employee_timesheets.push(employee_timesheet);
        }
    },

    /**
     * Remove the supplied Timesheet from the state
     *
     * @param state
     * @param timesheet
     * @constructor
     */
    REMOVE_EMPLOYEE_TIMESHEET (state, timesheet) {
        const employee_id = timesheet.employee_id;
        const timesheet_id = timesheet.timesheet_id;

        const index = state.employee_timesheets.findIndex((employee_timesheet) => employee_timesheet.timesheet_id === timesheet_id && employee_timesheet.employee_id === employee_id);

        if (index >= 0) {
            state.employee_timesheets.splice(index, 1)
        }
    },

    /**
     * @param state
     * @param employee_timesheet_entry
     * @constructor
     */
    ADD_EMPLOYEE_TIMESHEET_ENTRY (state, employee_timesheet_entry) {
        const employee_id = employee_timesheet_entry.employee_id;
        const date = employee_timesheet_entry.date;
        const start = employee_timesheet_entry.start;

        const index = state.employee_timesheet_entries.findIndex((employee_timesheet_entry) =>
            employee_timesheet_entry.employee_id === employee_id &&
            employee_timesheet_entry.date === date &&
            employee_timesheet_entry.start === start
        );

        if (employee_timesheet_entry.hasOwnProperty('created')) {
            let created = employee_timesheet_entry.created;
            employee_timesheet_entry['created'] = new Date(Date.parse(created)).toLocaleDateString('en-GB', {dateStyle: 'medium', timeStyle: 'medium'});
        }

        if (index >= 0) {
            Vue.set(state.employee_timesheet_entries, index, employee_timesheet_entry);
        } else {
            state.employee_timesheet_entries.push(employee_timesheet_entry);
        }
    },

    /**
     * Remove the specified Timesheet Entry.
     *
     * @param state
     * @param entry
     * @constructor
     */
    REMOVE_EMPLOYEE_TIMESHEET_ENTRY (state, entry) {

    },
};


/**
 * @type {{employees: (function(*): (Array|getters.employees|(function(*))|employees_component.computed.employees|{mutations, state, getters, actions, namespaced})), employee: (function(*): function(*): any)}}
 */
const getters = {
    /**
     * Return the Employees
     *
     * @param state
     * @returns {getters.employees|(function(*))|Array|{mutations, state, getters, actions, namespaced}|employees_component.computed.employees|(function(*): (Array|getters.employees|(function(*))|employees_component.computed.employees|{mutations, state, getters, actions, namespaced}))}
     */
    employees: (state) => (group_id=null) => {
        if (group_id) {
            return state.employees.filter((employee) => employee.parent_group_id === group_id);
        }
        return state.employees;
    },
    /**
     * Return the Employee identified by employee_id
     *
     * @param state
     * @returns {function(*): any}
     */
    employee: (state) => (employee_id) => {
        const employees = state.employees.filter((employee) => employee.employee_id === employee_id);
        return (employees.length === 1) ? employees[0] : {employee_id: null};
    },
    /**
     * Return the Timesheets that belong to the Employee specified by the supplied employee_id
     *
     * @param state
     * @returns {function(*): *[]}
     */
    employee_timesheets: (state) => (employee_id) => {
        return state.employee_timesheets.filter((timesheet) => timesheet.employee_id === employee_id);
    },
    /**
     * Return the Timesheet for the specified employee_id and date
     *
     * @param state
     * @returns {function({employee_id: *, date: *}): T[]}
     */
    employee_timesheet: (state) => ({employee_id, date}) => {
        const employee_timesheets = state.employee_timesheets.filter( (timesheet) => { return timesheet.date === date && timesheet.employee_id === employee_id; });
        return (employee_timesheets.length === 1) ? employee_timesheets[0]: {};
    },
    /**
     * Return the Contracts that belong to the Employee specified by the supplied employee_id
     *
     * @param state
     * @returns {function(*): T[]}
     */
    employee_contracts: (state) => (employee_id) => {
        return state.employee_contracts.filter((contract) => contract.employee_id === employee_id);
    },

    /**
     * @param state
     * @returns {function({employee_id: *, start_date: *}): any}
     */
    employee_contract: (state) => ({employee_id, start_date}) => {
        const employee_contracts = state.employee_contracts.filter( (contract) => { return contract.start_date === start_date && contract.employee_id === employee_id; });
        return employee_contracts.length === 1 ? employee_contracts[0]: {};
    },

    /**
     * @param state
     * @returns {function({employee_id: *, date: *}): T[]}
     */
    employee_timesheet_entries: (state) => ({employee_id, date}) => {
        return state.employee_timesheet_entries.filter( (entry) => { return entry.date === date && entry.employee_id === employee_id; });
    },

    /**
     * Return the list of Employees that belong to the specified Group.
     *
     * @param state
     * @returns {function(*): T[]}
     */
    group_employees: (state) => (group_id) => {
        return state.employees.filter((employee) => employee.parent_group_id === group_id);
    },
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}