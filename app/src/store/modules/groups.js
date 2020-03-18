import Vue from 'vue'
import groups from '../../api/groups'

/**
 * @type {{groups: Array}}
 */
const state = {
    groups: [],

    group_groups: [],

    group_employees: []
};

/**
 * @type {{employee_groups(*=): *, get_group(*=, *=): *, post_group(*=, *=): *}}
 */
const actions = {
    /**
     * Retrieve the Groups from the api
     *
     * @param context
     * @returns {Promise<any>}
     */
    get_groups (context) {
        return new Promise((resolve, reject) => {
            if (context.getters['groups'].length > 0) {
                resolve();
                return;
            }
            groups.groups_get()
                .then((response) => {
                    response.forEach((group) => {
                        context.commit('ADD_GROUP', group)
                    });
                    resolve();
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    /**
     * Post an Group to the api
     *
     * @param context
     * @param group
     * @returns {Promise<any>}
     */
    post_group (context, group) {
        return new Promise((resolve, reject) => {
            groups.groups_post(group)
                .then((group) => {
                    context.commit('ADD_GROUP', group);
                    resolve();
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    /**
     * Retrieve the Group identified by the supplied group_id
     *
     * @param context
     * @param group_id
     * @returns {Promise<any>}
     */
    get_group(context, group_id) {
        return new Promise((resolve, reject) => {
            groups.group_get(group_id)
                .then((group) => {
                    context.commit('ADD_GROUP', group);
                    resolve();
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    /**
     * Delete the Group
     *
     * @param context
     * @param group
     * @returns {Promise<any>}
     */
    delete_group(context, group) {
        return new Promise((resolve, reject) => {
            const group_id = group.group_id;
            groups.group_delete(group_id)
                .then((group) => {
                    context.commit('REMOVE_GROUP', group);
                    resolve();
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },

    /**
     * Retrieve the Groups that belong to the Group identified by the supplied
     * group_id.
     *
     * @param context
     * @param group_id
     * @returns {Promise<any>}
     */
    get_group_groups (context, group_id) {
        return new Promise((resolve, reject) => {
            groups.group_groups_get(group_id)
                .then((response) => {
                    response.forEach((sub_group) => {
                        context.commit('ADD_GROUP_GROUP', sub_group);
                    });
                    resolve();
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    // /**
    //  * Retrieve the Employees that belong to the Group identified by the supplied group_id
    //  *
    //  * @param context
    //  * @param group_id
    //  * @returns {Promise<any>}
    //  */
    // get_group_employees (context, group_id) {
    //     return new Promise((resolve, reject) => {
    //         groups.group_employees_get(group_id)
    //             .then((response) => {
    //                 response.forEach((employee) => {
    //                     context.commit('ADD_GROUP_EMPLOYEE', employee);
    //                 });
    //                 resolve();
    //             })
    //             .catch((error) => {
    //                 reject(error);
    //             });
    //     });
    // }
};

/**
 * @type {{ADD_GROUP(*, *=): void}}
 */
const mutations = {
    /**
     * Add an Group to the state
     *
     * @param state
     * @param group
     * @constructor
     */
    ADD_GROUP (state, group) {
        const group_id = group.group_id;
        const index = state.groups.findIndex((group) => group.group_id === group_id);

        if (group.hasOwnProperty('created')) {
            let created = group.created;
            group['created'] = new Date(Date.parse(created)).toLocaleDateString('en-GB', {dateStyle: 'medium', timeStyle: 'medium'});
        }

        if (group.hasOwnProperty('name')) {
            let name = group.name;
            let initials = name.match(/\b\w/g).join('');

            let colors = [
                'pink', 'purple', 'deep-purple', 'blue', 'light-blue', 'cyan',
                'teal', 'green', 'light-green', 'lime', 'yellow', 'amber', 'orange',
                'deep-orange', 'blue-grey'
            ];
            // @link https://stackoverflow.com/questions/4550505/getting-a-random-value-from-a-javascript-array
            let color = colors[Math.floor(Math.random() * colors.length)];

            group['color'] = color;
            group['initials'] = initials;
        }

        if (index >= 0) {
            Vue.set(state.groups, index, group);
        } else {
            state.groups.push(group);
        }
    },

    ADD_GROUP_GROUP (state, sub_group) {
        const group_id = sub_group.group_id;
        const sub_group_id = sub_group.sub_group_id;

        const index = state.group_groups.findIndex((group) =>
            group.group_id === group_id &&
            group.sub_group_id === sub_group_id
        );

        if (sub_group.hasOwnProperty('created')) {
            let created = sub_group.created;
            sub_group['created'] = new Date(Date.parse(created)).toLocaleDateString('en-GB', {dateStyle: 'medium', timeStyle: 'medium'});
        }

        if (index >= 0) {
            Vue.set(state.group_groups, index, sub_group);
        } else {
            state.group_groups.push(sub_group);
        }
    },

    ADD_GROUP_EMPLOYEE (state, employee) {
        const group_id = employee.group_id;
        const employee_id = employee.employee_id;

        const index = state.group_employees.findIndex((employee) =>
            employee.group_id === group_id &&
            employee.employee_id === employee_id
        );

        if (employee.hasOwnProperty('created')) {
            let created = employee.created;
            employee['created'] = new Date(Date.parse(created)).toLocaleDateString('en-GB', {dateStyle: 'medium', timeStyle: 'medium'});
        }

        if (index >= 0) {
            Vue.set(state.group_employees, index, employee);
        } else {
            state.group_employees.push(employee);
        }
    }
};

/**
 * @type {{employee_group: (function(*): function(*): any), employee_groups: (function(*): (getters.employee_groups|(function(*))|Array|state.employee_groups|{records, _meta}|employee_groups_component.computed.employee_groups|*))}}
 */
const getters = {
    /**
     * @param state
     * @returns {getters.employee_groups|(function(*))|Array|state.employee_groups|{records, _meta}|employee_groups_component.computed.employee_groups|*}
     */
    groups: (state) => {
        return state.groups;
    },
    /**
     * @param state
     * @returns {function(*): any}
     */
    group: (state) => (group_id) => {
        let groups = state.groups.filter((group) => group.group_id === group_id);
        return (groups.length === 1) ? groups[0] : {group_id: null};
    },

    /**
     *
     * @param state
     * @returns {function(*): Array}
     */
    group_groups: (state) => (group_id) => {
        return state.group_groups.filter((group) => group.parent_group_id === group_id);
    },

    // /**
    //  *
    //  * @param state
    //  * @returns {function(*): T[]}
    //  */
    // group_employees: (state) => (group_id) => {
    //     return state.group_employees.filter((employee) => employee.parent_group_id === group_id);
    // },
};

export default {
    namespaced: true,
    state,
    actions,
    mutations,
    getters
};