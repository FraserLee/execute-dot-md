local a = {1, nil, "test"}

for key, value in pairs(a) do
  local b = value and print(value)
end