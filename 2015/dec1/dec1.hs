pt1 :: String -> Int
pt1 s = moveFloor s

pt2 :: String -> Int
pt2 s = findBasement s 0

moveFloor :: String -> Int
moveFloor ('(':t) = 1 + moveFloor t
moveFloor (')':t) = -1 + moveFloor t
moveFloor [] = 0
moveFloor _ = 0

-- (Input String, Floor -> Position)
findBasement :: String -> Int -> Int
findBasement s (-1) = 0
findBasement ('(':t) f = 1 + findBasement t (f+1)
findBasement (')':t) f = 1 + findBasement t (f-1)
findBasement s p = 0


main :: IO ()
main = do
  contents <- readFile "input.txt"
  let result = pt1 contents
  print result

main2 = do
  contents <- readFile "input.txt"
  let result = pt2 contents
  print result

