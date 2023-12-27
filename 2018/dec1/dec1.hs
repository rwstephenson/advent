import Data.Set (Set,insert,member,empty)

parseInt :: String -> Int
parseInt ('+':num) = read num
parseInt num       = read num

sumFile :: [String] -> Int
sumFile entries = sum (map parseInt entries)

findRepeat :: Int -> Set Int -> [Int] -> Int
findRepeat total seen (num:rest) | member total seen = total
                                 | otherwise         = findRepeat (total+num) (insert total seen) rest
findRepeat _ _ _                                     = -1337

pt1 :: IO ()
pt1 = do
  contents <- readFile "input.txt"
  let entries = lines contents
  let result = sumFile entries
  print result

pt2 :: IO ()
pt2 = do
  contents <- readFile "input.txt"
  let entries = lines contents
  let result = findRepeat 0 empty (cycle (map parseInt entries))
  print result

