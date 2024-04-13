-- This script rescales CPT files for Generic Mapping Tools (GMT) input
-- Author: R Nate Crummett 3.30.24
------------------------------------------------------
-- Edit these varables
local rescaled_path = "Oasis-Montaj-Colors/arizona-magnetics.cpt" -- Path to ouput file, writing / overwriting
local reference_path = "Oasis-Montaj-Colors/geosoft-reference.cpt" -- Path to reference colormap, read only
local min_value = -400.0 -- Minimum decimal value in colormap
local max_value = 400.0  -- Maximum decimal value in colormap

------------------------------------------------------
-- NO EDITS NECESSARY BELOW THIS LINE
------------------------------------------------------

-- String splitting function, returns a table
function split(str, sep)
  -- Default seperation is whitespace
  if sep == nil then
    sep = "%s"
  end
  -- Split input string with sep
  local t = {}
  for s in string.gmatch(str, "([^" .. sep .. "]+)") do
    table.insert(t, s)
  end
  return t
end

-- Magic constants
local regular_legnth = 5 -- Length of lines defining regular colormap
local special_length = 2 -- Length of lines defining end, top, and nil colormaps

-- Count lines with five entries
local reference_file = io.open(reference_path, "r")

local line_count = 0
for line in reference_file:lines() do
  local split_line = split(line)

  if #split_line == 5 then
    line_count = line_count + 1
  end
end

reference_file:close()

-- Write new CPT file
reference_file = io.open(reference_path, "r")
local rescaled_file = io.open(rescaled_path, "w")
local range = max_value - min_value

local count = 0
for line in reference_file:lines() do
  local split_line = split(line)
  
  -- Determine line type, rescale the decimal values
  if #split_line == 5 then
    bot_rgb = split_line[2]
    top_rgb = split_line[4]
    code = split_line[5]
    
    local bot_val = range * (count / line_count) + min_value
    local top_val = range * ((count + 1) / line_count) + min_value
    
    newline = tostring(bot_val) .. " " .. bot_rgb .. " " .. 
      tostring(top_val) .. " " .. top_rgb .. " ".. code

    count = count + 1
  elseif #split_line == 2 then
    newline = split_line[1] .. " " .. split_line[2]
  else
    error("Invalid number of elements in this line")
  end

  -- Write the new line
  rescaled_file:write(newline .. "\n")
end

rescaled_file:close()
reference_file:close()
