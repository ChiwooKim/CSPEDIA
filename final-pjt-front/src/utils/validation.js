const isValidUsername = username => {
  if (!username.trim()) {
    return false
  } else if (username.length > 50) {
    return false
  }
  return true
}