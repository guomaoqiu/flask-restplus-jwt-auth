import request from '@/utils/request'

// export function loginByUsername(username, password) {
//   const data = {
//     username,
//     password
//   }
//   return request({
//     url: '/login/login',
//     method: 'post',
//     data
//   })
// }

export function loginByEmail(email, password) {
  const data = {
    email,
    password
  }
  return request({
    url: '/auth/login',
    method: 'post',
    data
  })
}

export function logout(token) {
  return request({
    url: '/auth/logout',
    method: 'post'
    // data
  })
}

export function getUserInfo(token) {
  return request({
    url: '/user/info',
    method: 'get',
    params: { token }
  })
}

