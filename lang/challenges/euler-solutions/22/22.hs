import qualified Data.Text as T
import Data.List
import Data.Char
import System.IO

genericEnumerate :: (Integral a) => a -> [b] -> [(a, b)]
genericEnumerate _ [] = []
genericEnumerate index (x:xs) = [(index, x)] ++ (genericEnumerate (succ index) xs)

enumerate :: (Integral a) => [b] -> [(a, b)]
enumerate = genericEnumerate 1

splitAtComma :: T.Text -> [T.Text]
splitAtComma s = T.splitOn (T.pack ",") s

stripDoubleQuotes :: T.Text -> T.Text
stripDoubleQuotes s = T.dropAround (== '"') s

letterToNumber :: Char -> Int
letterToNumber c = ord c - 64

scoreName :: (Int, T.Text) -> Int
scoreName (pos,name) = pos * (sum $ map letterToNumber $ T.unpack name)

parseFileContent :: T.Text -> [T.Text]
parseFileContent contents = sort $ map (stripDoubleQuotes . T.strip) $ splitAtComma contents

main = do
    contents <- readFile "names.txt"
    let names = parseFileContent $ T.pack contents
    print $ sum $ map scoreName $ enumerate names
