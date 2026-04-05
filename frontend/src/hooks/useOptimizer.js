import { useMutation } from '@tanstack/react-query'
import { post } from '../api/client'

export function useOptimizer() {
    return useMutation({
        mutationFn: ({ courses, preferences }) => post('/optimize', { course_codes: courses.map(c => c.course_code), preferences }),
    })
}