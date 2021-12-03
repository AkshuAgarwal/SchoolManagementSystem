export const getDashboardType = userType => {
    if (userType === 's') {
        return '/student/dashboard';
    } else if (userType === 't') {
        return '/teacher/dashboard';
    } else if (userType === 'p') {
        return '/parent/dashboard';
    } else if (userType === 'm') {
        return '/manager/dashboard';
    } else if (userType === 'a') {
        return '/admin/dashboard';
    };
};