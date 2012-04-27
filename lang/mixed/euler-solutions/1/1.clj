; (c) Florian Mayer <flormayer@aim.com> under the ISC license.
; See COPYING for more details.

(defn divides? [n x] (zero? (rem x n)))
(defn any-divides? [ns x] (some #(divides? % x) ns))
(defn get-divided [ns lst] (filter (partial any-divides? ns) lst))

(def sum (partial apply +))
(println (sum (get-divided [3 5] (range 1000))))
