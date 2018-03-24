const Acl = {
    install (Vue, options) {
        Vue.directive('can', {
            bind (el, binding, vnode, oldVnode) {
                var permission = binding.value
                var uprofile = window.userProfile
                if (!uprofile.isSuperUser && uprofile.permissions.indexOf(permission) === -1) {
                    el.style.display = 'none'
                }
            }
        })

        Vue.prototype.$can = function (permission) {
            var uprofile = window.userProfile
            if (uprofile.isSuperUser || uprofile.permissions.indexOf(permission) !== -1) {
                return true
            }
            return false
        }
    }
}

module.exports = Acl
