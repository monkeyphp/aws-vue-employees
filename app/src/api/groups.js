/**
 * @file groups.js
 */
import axios from 'axios';
/* eslint-disable */

export default {
    /**
     * Return a list of Groups
     *
     * @returns {Promise<any>}
     */
    groups_get() {
        return new Promise((resolve, reject) => {
            axios.get(`/groups`)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    /**
     * Post an Group
     *
     * @param group
     * @returns {Promise<any>}
     */
    groups_post (group) {
        return new Promise((resolve, reject) => {
            axios.post(`/groups`, group)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    if (error.response) {
                        const data = error.response.data;
                        reject(data);
                    }
                    reject(error);
                });
        });
    },

    /**
     * Return the Group identified by the supplied group_id
     *
     * @param group_id
     * @returns {Promise<any>}
     */
    group_get (group_id) {
        return new Promise((resolve, reject) => {
            axios.get(`/groups/${group_id}`)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },

    /**
     * Delete the Group identified by the supplied group_id
     *
     * @param group_id
     * @returns {Promise<any>}
     */
    group_delete(group_id) {
        return new Promise((resolve, reject) => {
            axios.delete(`/groups/${group_id}`)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    /**
     * Return the Groups that have been added to the Group identified by the
     * supplied group_id
     *
     * @param group_id
     * @returns {Promise<any>}
     */
    group_groups_get (group_id) {
        return new Promise((resolve, reject) => {
            axios.get(`/groups/${group_id}/groups`)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    // /**
    //  * Post an Group as a child/sub of the EmployeeGroup identified by the supplied
    //  * employee_group_id
    //  *
    //  * @param employee_group_id
    //  * @param employee_group
    //  * @returns {Promise<any>}
    //  */
    // employee_group_employee_groups_post(employee_group_id, employee_group) {
    //     return new Promise((resolve, reject) => {
    //         axios.post(`/employee-groups/${employee_group_id}/employee-groups`, employee_group)
    //             .then((response) => {
    //                 const data = response.data;
    //                 resolve(data);
    //             })
    //             .catch((error) => {
    //                 reject(error);
    //             })
    //     });
    // },
    /**
     * Return the Employees that have been added to the EmployeeGroup identified by the
     * supplied employee_group_id
     *
     * @param employee_group_id
     * @returns {Promise<any>}
     */
    group_employees_get (group_id) {
        return new Promise((resolve, reject) => {
            axios.get(`/groups/${group_id}/employees`)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    /**
     * Add an Employee to the specified EmployeeGroup
     *
     * @param employee_group_id
     * @param employee
     * @returns {Promise<any>}
     */
    // employee_group_employees_post(employee_group_id, employee) {
    //     return new Promise((resolve, reject) => {
    //         axios.post(`/employee-groups/${employee_group_id}/employees`, employee)
    //             .then((response) => {
    //                 const data = response.data;
    //                 resolve(data);
    //             })
    //             .catch((error) => {
    //                 reject(error);
    //             });
    //     });
    // }
};
