


main :: IO ()
main = do
    let input = map (read :: Int) $ lines getContents
    putStrLn . fmap sum 